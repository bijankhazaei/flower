import React from 'react';
import { cn } from '@/utilities/helpers';
import { NodeProps } from '@/contracts/components';

export const Node: React.FC<NodeProps> = ({
  node,
  isSelected,
  onDrag,
  onClick
}) => {
  const handleMouseDown = (e: React.MouseEvent) => {
    e.preventDefault();
    const startX = e.clientX;
    const startY = e.clientY;
    
    const handleMouseMove = (e: MouseEvent) => {
      const deltaX = e.clientX - startX;
      const deltaY = e.clientY - startY;
      onDrag?.({ x: deltaX, y: deltaY });
    };
    
    const handleMouseUp = () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
    
    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);
  };

  return (
    <div
      className={cn(
        'absolute bg-white border-2 rounded-lg shadow-md cursor-pointer min-w-[150px] min-h-[80px] transition-all',
        isSelected ? 'border-dominant-500 shadow-lg' : 'border-gray-300',
        'hover:shadow-lg'
      )}
      style={{
        transform: `translate(${node.position.x}px, ${node.position.y}px)`
      }}
      onClick={() => onClick?.(node.id)}
      onMouseDown={handleMouseDown}
    >
      {/* Node Header */}
      <div className="px-3 py-2 bg-gray-100 rounded-t-lg border-b">
        <h3 className="text-sm font-medium text-gray-900">
          {node.type}
        </h3>
      </div>
      
      {/* Node Body */}
      <div className="p-3">
        <div className="text-xs text-gray-600">
          ID: {node.id}
        </div>
        {node.config && Object.keys(node.config).length > 0 && (
          <div className="mt-2 text-xs">
            <div className="font-medium">Config:</div>
            <div className="text-gray-500 max-w-[120px] truncate">
              {JSON.stringify(node.config)}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};