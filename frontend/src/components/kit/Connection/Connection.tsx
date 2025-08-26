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
    <path
      d={path}
      stroke="#6b7280"
      strokeWidth="2"
      fill="none"
      className="pointer-events-none"
    />
  );
};