import React from 'react';
import { FlowCanvas } from '@/components/ui/FlowCanvas/FlowCanvas';
import { NodePalette } from '@/components/ui/NodePalette/NodePalette';
import { PropertyPanel } from '@/components/ui/PropertyPanel/PropertyPanel';
import { Toolbar } from '@/components/ui/Toolbar/Toolbar';

const FlowEditor: React.FC = () => {
  return (
    <div className="h-full flex flex-col">
      <Toolbar />
      
      <div className="flex-1 flex">
        <div className="flex-shrink-0">
          <NodePalette />
        </div>
        
        <div className="flex-1">
          <FlowCanvas />
        </div>
        
        <div className="flex-shrink-0">
          <PropertyPanel />
        </div>
      </div>
    </div>
  );
};

export default FlowEditor;