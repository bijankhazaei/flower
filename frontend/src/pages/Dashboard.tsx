import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FlowList } from '@/components/ui/FlowList/FlowList';
import { Flow } from '@/contracts/api';

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const [flows] = useState<Flow[]>([
    {
      id: '1',
      name: 'Sample Flow',
      description: 'A sample flow for demonstration',
      nodes: [],
      connections: [],
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    }
  ]);

  const handleFlowSelect = (flow: Flow) => {
    navigate(`/flow-editor/${flow.id}`);
  };

  const handleFlowCreate = () => {
    navigate('/flow-editor/new');
  };

  const handleFlowDelete = (flowId: string) => {
    console.log('Delete flow:', flowId);
  };

  return (
    <FlowList
      flows={flows}
      onFlowSelect={handleFlowSelect}
      onFlowCreate={handleFlowCreate}
      onFlowDelete={handleFlowDelete}
    />
  );
};

export default Dashboard;