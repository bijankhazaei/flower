import React from 'react';
import { ConnectionProps } from '@/contracts/components';

export const Connection: React.FC<ConnectionProps> = ({
  connection,
  nodes
}) => {
  const sourceNode = nodes[connection.source];
  const targetNode = nodes[connection.target];
  
  if (!sourceNode || !targetNode) return null;
  
  const sourceX = sourceNode.position.x + 150; // Node width
  const sourceY = sourceNode.position.y + 40;  // Node height / 2
  const targetX = targetNode.position.x;
  const targetY = targetNode.position.y + 40;
  
  // Create bezier curve path
  const controlPoint1X = sourceX + (targetX - sourceX) / 3;
  const controlPoint2X = targetX - (targetX - sourceX) / 3;
  
  const path = `M ${sourceX} ${sourceY} C ${controlPoint1X} ${sourceY} ${controlPoint2X} ${targetY} ${targetX} ${targetY}`;
  
  return (
    <g>
      <defs>
        <marker
          id="arrowhead"
          markerWidth="10"
          markerHeight="7"
          refX="9"
          refY="3.5"
          orient="auto"
        >
          <polygon
            points="0 0, 10 3.5, 0 7"
            fill="#6b7280"
          />
        </marker>
      </defs>
      <path
        d={path}
        stroke="#6b7280"
        strokeWidth="2"
        fill="none"
        markerEnd="url(#arrowhead)"
        className="hover:stroke-dominant-500 cursor-pointer transition-colors"
      />
    </g>
  );
};