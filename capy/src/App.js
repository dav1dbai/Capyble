import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import Todo from './components/todo'
//import Chatbot from './components/Chatbot'
import Calendar from './components/calendar'
import Navigation from './components/navigation';

function App() {
  const handleToggleWindow = () => {
    // Accessing the exposed API in renderer process
    console.log("pressed")
    window.api.send("")
    window.api.receive('fromMain', (data) => {
    console.log(`Received: ${data}`);
});

window.api.send('toMain', 'some data');

  };

  return (
    <Router>
      <div>
        <Navigation />
        <button
          onClick={handleToggleWindow}
          style={{
            position: 'fixed',
            left: '0%',
            top: '50%',
            transform: 'translate(-50%, -50%)',
            zIndex: 9999,
          }}
        >
          Toggle Window
        </button>
        <Routes>
          <Route path="/todo" element={<Todo/>} />
          <Route path="/chat" element={<Todo/>}/>
          <Route path="/cal" element={<Calendar/>}/>
        </Routes>
      </div>
    </Router>
  );
}

export default App;