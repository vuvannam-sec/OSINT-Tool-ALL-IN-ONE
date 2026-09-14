import React, { useMemo, useState } from 'react';
import { Maximize2, RotateCcw, ZoomIn, ZoomOut } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface NetworkDiagramProps {
  data: any;
  width?: number;
  height?: number;
}

interface GraphNode {
  id: string;
  label: string;
  depth: number;
  parentId?: string;
  profileUrl?: string;
}

const NODE_WIDTH = 150;
const NODE_HEIGHT = 42;
const X_GAP = 40;
const Y_GAP = 90;

function asString(value: unknown): string | undefined {
  if (value === null || value === undefined) return undefined;
  const result = String(value).trim();
  return result || undefined;
}

function normalizeRoot(data: any): any | null {
  if (!data) return null;
  const tree = Array.isArray(data.tree_data) ? data.tree_data[0] : data.tree_data;
  return tree && typeof tree === 'object' ? tree : null;
}

function flattenTree(root: any): GraphNode[] {
  const nodes: GraphNode[] = [];
  const visited = new Set<string>();

  const walk = (node: any, depth: number, parentId?: string) => {
    if (!node || typeof node !== 'object') return;

    const id = asString(node.id ?? node.username ?? node.profile_id);
    if (!id || visited.has(id)) return;
    visited.add(id);

    nodes.push({
      id,
      label: asString(node.title ?? node.name ?? node.username) ?? id,
      depth,
      parentId,
      profileUrl: asString(node.profile_url ?? node.url),
    });

    const children = Array.isArray(node.children) ? node.children : [];
    children.forEach((child: any) => walk(child, depth + 1, id));
  };

  walk(root, 0);
  return nodes;
}

export const NetworkDiagram: React.FC<NetworkDiagramProps> = ({
  data,
  width = 800,
  height = 560,
}) => {
  const [zoom, setZoom] = useState(1);

  const nodes = useMemo(() => flattenTree(normalizeRoot(data)), [data]);

  const layout = useMemo(() => {
    const byDepth = new Map<number, GraphNode[]>();
    nodes.forEach((node) => {
      const level = byDepth.get(node.depth) ?? [];
      level.push(node);
      byDepth.set(node.depth, level);
    });

    const maxPerLevel = Math.max(1, ...Array.from(byDepth.values()).map((level) => level.length));
    const maxDepth = Math.max(0, ...nodes.map((node) => node.depth));
    const canvasWidth = Math.max(width, maxPerLevel * (NODE_WIDTH + X_GAP) + X_GAP);
    const canvasHeight = Math.max(height, (maxDepth + 1) * (NODE_HEIGHT + Y_GAP) + Y_GAP);
    const positions = new Map<string, { x: number; y: number }>();

    byDepth.forEach((level, depth) => {
      const step = canvasWidth / (level.length + 1);
      level.forEach((node, index) => {
        positions.set(node.id, {
          x: step * (index + 1),
          y: Y_GAP + depth * (NODE_HEIGHT + Y_GAP),
        });
      });
    });

    return { canvasWidth, canvasHeight, positions };
  }, [height, nodes, width]);

  if (nodes.length === 0) {
    return (
      <div className="flex min-h-[260px] items-center justify-center rounded-lg border border-white/10 bg-black/20 p-6 text-sm text-gray-400">
        Network data will appear here after a successful crawl.
      </div>
    );
  }

  const changeZoom = (next: number) => setZoom(Math.min(2, Math.max(0.5, next)));

  return (
    <div className="overflow-hidden rounded-lg border border-white/10 bg-black/20">
      <div className="flex items-center justify-between border-b border-white/10 px-3 py-2">
        <div className="text-sm text-gray-300">
          {nodes.length} account{nodes.length === 1 ? '' : 's'}
        </div>
        <div className="flex gap-1">
          <Button variant="ghost" size="icon" onClick={() => changeZoom(zoom - 0.1)} aria-label="Zoom out">
            <ZoomOut className="h-4 w-4" />
          </Button>
          <Button variant="ghost" size="icon" onClick={() => setZoom(1)} aria-label="Reset zoom">
            <RotateCcw className="h-4 w-4" />
          </Button>
          <Button variant="ghost" size="icon" onClick={() => changeZoom(zoom + 0.1)} aria-label="Zoom in">
            <ZoomIn className="h-4 w-4" />
          </Button>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => document.documentElement.requestFullscreen?.()}
            aria-label="Enter fullscreen"
          >
            <Maximize2 className="h-4 w-4" />
          </Button>
        </div>
      </div>

      <div className="overflow-auto" style={{ maxHeight: height }}>
        <svg
          width={layout.canvasWidth * zoom}
          height={layout.canvasHeight * zoom}
          viewBox={`0 0 ${layout.canvasWidth} ${layout.canvasHeight}`}
          role="img"
          aria-label="OSINT account relationship graph"
        >
          <g>
            {nodes.map((node) => {
              if (!node.parentId) return null;
              const from = layout.positions.get(node.parentId);
              const to = layout.positions.get(node.id);
              if (!from || !to) return null;

              return (
                <line
                  key={`${node.parentId}-${node.id}`}
                  x1={from.x}
                  y1={from.y + NODE_HEIGHT / 2}
                  x2={to.x}
                  y2={to.y - NODE_HEIGHT / 2}
                  stroke="currentColor"
                  className="text-white/20"
                  strokeWidth="1.5"
                />
              );
            })}

            {nodes.map((node) => {
              const position = layout.positions.get(node.id);
              if (!position) return null;

              return (
                <g key={node.id} transform={`translate(${position.x}, ${position.y})`}>
                  <rect
                    x={-NODE_WIDTH / 2}
                    y={-NODE_HEIGHT / 2}
                    width={NODE_WIDTH}
                    height={NODE_HEIGHT}
                    rx="8"
                    className="fill-slate-900 stroke-white/20"
                  />
                  <text
                    textAnchor="middle"
                    dominantBaseline="middle"
                    className="fill-slate-100 text-[12px]"
                  >
                    {node.label.length > 21 ? `${node.label.slice(0, 20)}…` : node.label}
                  </text>
                  <title>
                    {node.profileUrl ? `${node.label}\n${node.profileUrl}` : node.label}
                  </title>
                </g>
              );
            })}
          </g>
        </svg>
      </div>
    </div>
  );
};
