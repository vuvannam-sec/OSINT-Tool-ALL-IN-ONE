import React, { useMemo } from 'react';

interface NetworkDiagramProps {
  data: any;
  width?: number;
  height?: number;
}

interface PositionedNode {
  key: string;
  label: string;
  subtitle?: string;
  x: number;
  y: number;
  depth: number;
  parentKey?: string;
}

const getLabel = (node: any): string => {
  return String(node?.title || node?.name || node?.username || node?.id || 'Unknown');
};

const getSubtitle = (node: any): string | undefined => {
  const id = node?.username || node?.id;
  if (!id || String(id) === getLabel(node)) return undefined;
  return String(id);
};

const buildLayout = (root: any, width: number) => {
  if (!root || typeof root !== 'object') {
    return { nodes: [] as PositionedNode[], height: 260 };
  }

  const levels: any[][] = [];
  const queue: Array<{ node: any; depth: number; parentKey?: string; key: string }> = [
    { node: root, depth: 0, key: 'root' },
  ];
  const rawNodes: Array<{
    node: any;
    depth: number;
    parentKey?: string;
    key: string;
  }> = [];

  while (queue.length) {
    const current = queue.shift()!;
    rawNodes.push(current);
    levels[current.depth] ??= [];
    levels[current.depth].push(current);

    const children = Array.isArray(current.node?.children) ? current.node.children : [];
    children.forEach((child: any, index: number) => {
      queue.push({
        node: child,
        depth: current.depth + 1,
        parentKey: current.key,
        key: `${current.key}.${index}`,
      });
    });
  }

  const horizontalPadding = 72;
  const verticalSpacing = 145;
  const topPadding = 64;
  const chartHeight = Math.max(260, topPadding * 2 + (levels.length - 1) * verticalSpacing);

  const nodes: PositionedNode[] = rawNodes.map((entry) => {
    const level = levels[entry.depth];
    const index = level.findIndex((item) => item.key === entry.key);
    const usableWidth = Math.max(1, width - horizontalPadding * 2);
    const x = level.length === 1
      ? width / 2
      : horizontalPadding + (usableWidth * index) / (level.length - 1);

    return {
      key: entry.key,
      label: getLabel(entry.node),
      subtitle: getSubtitle(entry.node),
      x,
      y: topPadding + entry.depth * verticalSpacing,
      depth: entry.depth,
      parentKey: entry.parentKey,
    };
  });

  return { nodes, height: chartHeight };
};

export const NetworkDiagram: React.FC<NetworkDiagramProps> = ({
  data,
  width = 900,
  height = 600,
}) => {
  const treeData = data?.tree_data ?? data;
  const layout = useMemo(() => buildLayout(treeData, width), [treeData, width]);
  const nodesByKey = useMemo(
    () => new Map(layout.nodes.map((node) => [node.key, node])),
    [layout.nodes],
  );

  if (!treeData || layout.nodes.length === 0) {
    return (
      <div className="flex min-h-[260px] items-center justify-center rounded-lg border border-white/10 bg-black/20 p-8 text-sm text-gray-400">
        No network data available. Run a collector or load a JSON export first.
      </div>
    );
  }

  const canvasHeight = Math.max(height, layout.height);

  return (
    <div className="w-full overflow-auto rounded-lg border border-white/10 bg-black/20">
      <svg
        width={width}
        height={canvasHeight}
        viewBox={`0 0 ${width} ${canvasHeight}`}
        role="img"
        aria-label="Relationship network"
        className="block min-w-full"
      >
        <g stroke="currentColor" className="text-gray-700" strokeWidth="1.5">
          {layout.nodes.map((node) => {
            if (!node.parentKey) return null;
            const parent = nodesByKey.get(node.parentKey);
            if (!parent) return null;

            return (
              <line
                key={`${parent.key}-${node.key}`}
                x1={parent.x}
                y1={parent.y + 24}
                x2={node.x}
                y2={node.y - 24}
              />
            );
          })}
        </g>

        {layout.nodes.map((node) => (
          <g key={node.key} transform={`translate(${node.x}, ${node.y})`}>
            <circle
              r={node.depth === 0 ? 26 : 22}
              fill="currentColor"
              className={node.depth === 0 ? 'text-blue-500' : 'text-slate-600'}
              stroke="rgba(255,255,255,0.25)"
              strokeWidth="2"
            />
            <text
              y={node.depth === 0 ? 44 : 40}
              textAnchor="middle"
              className="fill-gray-100 text-[12px] font-medium"
            >
              {node.label.length > 28 ? `${node.label.slice(0, 27)}…` : node.label}
            </text>
            {node.subtitle && (
              <text
                y={node.depth === 0 ? 61 : 57}
                textAnchor="middle"
                className="fill-gray-500 text-[10px]"
              >
                {node.subtitle.length > 30 ? `${node.subtitle.slice(0, 29)}…` : node.subtitle}
              </text>
            )}
            <title>{node.subtitle ? `${node.label} (${node.subtitle})` : node.label}</title>
          </g>
        ))}
      </svg>
    </div>
  );
};

export default NetworkDiagram;
