import { useEffect } from 'react';
import { FlowCanvas } from '@/components/ui/FlowCanvas/FlowCanvas';
import { Resolver } from '@/modules/resolver/Resolver';
import { useCanvasStore } from '@/store/canvasStore';
import './App.css';

function App() {
  const { addNode } = useCanvasStore();
  
  // Add some demo nodes
  useEffect(() => {
    addNode({
      id: 'node-1',
      type: 'TextInput',
      position: { x: 100, y: 100 },
      config: { placeholder: 'Enter text' }
    });
    
    addNode({
      id: 'node-2', 
      type: 'TextProcessor',
      position: { x: 400, y: 150 },
      config: { operation: 'uppercase' }
    });
  }, [addNode]);
  
  return (
    <div className="h-screen flex flex-col">
      {/* Header */}
      <div className="h-16 bg-white border-b border-gray-200 flex items-center px-4">
        <h1 className="text-xl font-semibold text-gray-900">🌸 Flower</h1>
        <div className="ml-auto flex gap-2">
          <Resolver.Button variant="secondary" size="sm">
            Save
          </Resolver.Button>
          <Resolver.Button variant="primary" size="sm">
            Run Flow
          </Resolver.Button>
        </div>
      </div>
      
      {/* Main Content */}
      <div className="flex-1 flex">
        {/* Sidebar */}
        <div className="w-64 bg-white border-r border-gray-200 p-4">
          <h2 className="text-lg font-medium mb-4">Nodes</h2>
          <div className="space-y-2">
            <Resolver.Card padding="sm" className="cursor-pointer hover:bg-gray-50">
              <div className="text-sm font-medium">Text Input</div>
              <div className="text-xs text-gray-500">Input text data</div>
            </Resolver.Card>
            <Resolver.Card padding="sm" className="cursor-pointer hover:bg-gray-50">
              <div className="text-sm font-medium">Text Processor</div>
              <div className="text-xs text-gray-500">Process text</div>
            </Resolver.Card>
          </div>
        </div>
        
        {/* Canvas */}
        <div className="flex-1">
          <FlowCanvas />
        </div>
      </div>
    </div>
  );
}

export default App;