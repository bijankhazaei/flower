import React, { useCallback, useRef } from 'react';
import { Resolver } from '@/modules/resolver/Resolver';
import { useCanvasStore } from '@/store/canvasStore';
import { useCanvasInteractions } from '@/hooks/useCanvasInteractions';

export const FlowCanvas: React.FC = () => {
  const canvasRef = useRef<HTMLDivElement>(null);
  const {
    zoom,
    pan,
    nodes,
    connections,
    selection,
    mode,
    updateNode,
    selectNodes,
    clearSelection,
    setZoom,
    setPan
  } = useCanvasStore();
  
  const { handleWheel, handlePan } = useCanvasInteractions();
  
  const handleCanvasClick = useCallback(() => {
    clearSelection();
  }, [clearSelection]);
  
  const handleNodeClick = useCallback((nodeId: string) => {
    selectNodes([nodeId]);
  }, [selectNodes]);
  
  const handleNodeDrag = useCallback((nodeId: string, offset: { x: number; y: number }) => {
    const node = nodes[nodeId];
    if (node) {
      updateNode(nodeId, {
        position: {
          x: node.position.x + offset.x,
          y: node.position.y + offset.y
        }
      });
    }
  }, [nodes, updateNode]);
  
  return (
    <div 
      ref={canvasRef}
      className="relative w-full h-full"
      onWheel={handleWheel}
      onMouseDown={handlePan}
    >
      <Resolver.Canvas
        zoom={zoom}
        pan={pan}
        mode={mode}
        onCanvasClick={handleCanvasClick}
        className="w-full h-full"
      >
        {/* Connections layer */}
        <svg className="absolute inset-0 pointer-events-none">
          {Object.values(connections).map(connection => (
            <Resolver.Connection
              key={connection.id}
              connection={connection}
              nodes={nodes}
            />
          ))}
        </svg>
        
        {/* Nodes layer */}
        {Object.values(nodes).map(node => (
          <Resolver.Node
            key={node.id}
            node={node}
            isSelected={selection.includes(node.id)}
            onClick={handleNodeClick}
            onDrag={(offset) => handleNodeDrag(node.id, offset)}
          />
        ))}
      </Resolver.Canvas>
      
      {/* Canvas controls */}
      <div className="absolute bottom-4 right-4 flex flex-col gap-2">
        <Resolver.Button
          variant="secondary"
          size="sm"
          onClick={() => setZoom(1)}
        >
          Reset Zoom
        </Resolver.Button>
        <Resolver.Button
          variant="secondary"
          size="sm"
          onClick={() => setPan({ x: 0, y: 0 })}
        >
          Center
        </Resolver.Button>
        <div className="text-xs text-gray-500 bg-white px-2 py-1 rounded">
          {Math.round(zoom * 100)}%
        </div>
      </div>
    </div>
  );
};