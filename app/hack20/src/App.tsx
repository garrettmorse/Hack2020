import React from 'react';
import './App.css';
import { Menu } from 'semantic-ui-react';
import Listen from './components/Listen';

const App = () => {
  return (
    <div>
      <Menu><Menu.Item name='app'>My App</Menu.Item></Menu>
      <Listen />
    </div>
  );
}

export default App;
