import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import Todo from './components/todo'
import Chatbot from './components/Chatbot'
import Calendar from './components/calendar'
import Navigation from './components/navigation';

import checkedimg from './assets/mini_capy.png'

function App() {
  const handleToggleWindow = () => {
    // Accessing the exposed API in renderer process
    console.log("pressed");
    window.api.send('toggleWindow');
  };

  window.api.send('toMain', 'some data');

  return (
    <Router>
      <div>
        <Navigation />
        <button
          onClick={handleToggleWindow}
          style={{
            position: 'fixed',
            left: '10%',
            top: '90%',
            transform: 'translate(-50%, -50%)',
            zIndex: 100,
          }}
        >
          <img src={checkedimg} className='w-16 h-16'/>
        </button>
        <Routes>
          <Route path="/todo" element={<Todo/>} />
          <Route path="/" element={<Chatbot/>}/>
          <Route path="/cal" element={<Calendar/>}/>
        </Routes>
      </div>
    </Router>
  );
}

export default App;