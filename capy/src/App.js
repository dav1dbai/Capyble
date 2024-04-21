import {React, useEffect} from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import Todo from './components/todo'
import Chatbot from './components/Chatbot'
import Calendar from './components/calendar'
import Navigation from './components/navigation';

import checkedimg from './assets/checked.png'

function App() {
  const handleToggleWindow = () => {
    // Accessing the exposed API in renderer process
    console.log("pressed");
    window.api.send('toggleWindow');
  };

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    const response = await fetch('http://127.0.0.1:5000/sprites', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({request: "fetch"})  // Dummy payload if needed
    });
    const data = await response.json();
    console.log(data)
  };

  //window.api.send('toMain', 'some data');

  return (
    <Router>
      <div>
        <Navigation />
        <button
          onClick={handleToggleWindow}
          style={{
            position: 'fixed',
            left: '5%',
            top: '50%',
            transform: 'translate(-50%, -50%)',
            zIndex: 100,
          }}
        >
          <img src={checkedimg} className='w-8 h-8'/>
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