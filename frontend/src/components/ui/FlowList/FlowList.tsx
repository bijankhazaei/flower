import React, { useState } from 'react';
import { Resolver } from '@/modules/resolver/Resolver';
import { Flow } from '@/contracts/api';

interface FlowListProps {
  flows: Flow[];
  onFlowSelect: (flow: Flow) => void;
  onFlowCreate: () => void;
  onFlowDelete: (flowId: string) => void;
}

export const FlowList: React.FC<FlowListProps> = ({
  flows,
  onFlowSelect,
  onFlowCreate,
  onFlowDelete
}) => {
  const [searchTerm, setSearchTerm] = useState('');

  const filteredFlows = flows.filter(flow =>
    flow.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Flows</h1>
        <Resolver.Button onClick={onFlowCreate}>
          Create Flow
        </Resolver.Button>
      </div>

      <div className="mb-6">
        <Resolver.Input
          placeholder="Search flows..."
          value={searchTerm}
          onChange={setSearchTerm}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredFlows.map(flow => (
          <Resolver.Card key={flow.id} className="cursor-pointer hover:shadow-lg">
            <div className="p-4">
              <h3 className="font-semibold text-lg mb-2">{flow.name}</h3>
              {flow.description && (
                <p className="text-gray-600 text-sm mb-3">{flow.description}</p>
              )}
              <div className="flex justify-between items-center text-xs text-gray-500 mb-3">
                <span>{flow.nodes.length} nodes</span>
                <span>{new Date(flow.updated_at).toLocaleDateString()}</span>
              </div>
              <div className="flex gap-2">
                <Resolver.Button
                  variant="primary"
                  size="sm"
                  onClick={() => onFlowSelect(flow)}
                  className="flex-1"
                >
                  Open
                </Resolver.Button>
                <Resolver.Button
                  variant="destructive"
                  size="sm"
                  onClick={() => onFlowDelete(flow.id)}
                >
                  Delete
                </Resolver.Button>
              </div>
            </div>
          </Resolver.Card>
        ))}
      </div>

      {filteredFlows.length === 0 && (
        <div className="text-center py-12">
          <div className="text-gray-500 mb-4">
            {searchTerm ? 'No flows found' : 'No flows created yet'}
          </div>
          <Resolver.Button onClick={onFlowCreate}>
            Create Your First Flow
          </Resolver.Button>
        </div>
      )}
    </div>
  );
};