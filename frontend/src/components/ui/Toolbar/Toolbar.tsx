import React, { useState } from 'react';
import { Resolver } from '@/modules/resolver/Resolver';
import { useCanvasStore } from '@/store/canvasStore';
import { FlowCompiler } from '@/components/ui/FlowCompiler/FlowCompiler';
import { FlowExecutor } from '@/components/ui/FlowExecutor/FlowExecutor';

export const Toolbar: React.FC = () => {
  const { mode, setMode, clearCanvas, nodes, connections } = useCanvasStore();
  const [showCompiler, setShowCompiler] = useState(false);
  const [showExecutor, setShowExecutor] = useState(false);

  const handleSave = () => {
    const flowData = {
      nodes: Object.values(nodes),
      connections: Object.values(connections)
    };
    console.log('Saving flow:', flowData);
    // TODO: Implement actual save functionality
  };

  const handleLoad = () => {
    // TODO: Implement load functionality
    console.log('Load flow');
  };

  const handleExport = () => {
    const flowData = {
      nodes: Object.values(nodes),
      connections: Object.values(connections)
    };
    const dataStr = JSON.stringify(flowData, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'flow.json';
    link.click();
  };

  const handleRun = () => {
    setShowExecutor(true);
  };

  const handleCompile = () => {
    setShowCompiler(true);
  };

  return (
    <div className="flex items-center gap-2 p-3 bg-white border-b">
      {/* File operations */}
      <div className="flex items-center gap-1">
        <Resolver.Button variant="ghost" size="sm" onClick={handleSave}>
          Save
        </Resolver.Button>
        <Resolver.Button variant="ghost" size="sm" onClick={handleLoad}>
          Load
        </Resolver.Button>
        <Resolver.Button variant="ghost" size="sm" onClick={handleExport}>
          Export
        </Resolver.Button>
      </div>
      
      <div className="w-px h-6 bg-gray-300" />
      
      {/* Canvas modes */}
      <div className="flex items-center gap-1">
        <Resolver.Button
          variant={mode === 'select' ? 'primary' : 'ghost'}
          size="sm"
          onClick={() => setMode('select')}
        >
          Select
        </Resolver.Button>
        <Resolver.Button
          variant={mode === 'connect' ? 'primary' : 'ghost'}
          size="sm"
          onClick={() => setMode('connect')}
        >
          Connect
        </Resolver.Button>
        <Resolver.Button
          variant={mode === 'pan' ? 'primary' : 'ghost'}
          size="sm"
          onClick={() => setMode('pan')}
        >
          Pan
        </Resolver.Button>
      </div>
      
      <div className="w-px h-6 bg-gray-300" />
      
      {/* Flow operations */}
      <div className="flex items-center gap-1">
        <Resolver.Button
          variant="secondary"
          size="sm"
          onClick={handleCompile}
          disabled={Object.keys(nodes).length === 0}
        >
          Compile
        </Resolver.Button>
        <Resolver.Button
          variant="primary"
          size="sm"
          onClick={handleRun}
          disabled={Object.keys(nodes).length === 0}
        >
          Run Flow
        </Resolver.Button>
        <Resolver.Button
          variant="destructive"
          size="sm"
          onClick={clearCanvas}
        >
          Clear
        </Resolver.Button>
      </div>
      
      <div className="flex-1" />
      
      {/* Status */}
      <div className="text-sm text-gray-500">
        {Object.keys(nodes).length} nodes, {Object.keys(connections).length} connections
      </div>
      
      {/* Modals */}
      <FlowCompiler
        isOpen={showCompiler}
        onClose={() => setShowCompiler(false)}
      />
      <FlowExecutor
        isOpen={showExecutor}
        onClose={() => setShowExecutor(false)}
      />
    </div>
  );
};