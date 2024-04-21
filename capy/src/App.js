import {React, useEffect, useState} from 'react';
import { BrowserRouter as Router, Route, Routes, json } from 'react-router-dom';

import Todo from './components/todo'
import Chatbot from './components/Chatbot'
import Calendar from './components/calendar'
import Navigation from './components/navigation';

import checkedimg from './assets/mini_capy_right.png'

function App() {
  const [isOpen, setIsOpen] = useState(false);

  // Function to handle toggle, it sends a command to the window API and updates the state
  const handleToggleWindow = () => {
    const newIsOpen = !isOpen;  // Calculate the new state as the opposite of the current state
    const command = newIsOpen ? 'open' : 'close';  // Determine command based on the new state

    window.api.send('toggleWindow', command);  // Send the command to Electron's main process
    setIsOpen(newIsOpen);  // Update the component's state to the new state
  };

  /*
  const fetchData = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/sprites', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({request: "fetch"})  // Dummy payload for fetching current state
      });
      const jsonData = await response.json();
      console.log(jsonData.toggle_state)
      setIsOpen(jsonData.toggle_state);  // Update the local state with the fetched state
      window.api.send('toggleWindow', isOpen);
    } catch (error) {
      console.error('Failed to fetch data:', error);
    }
  };
  */

  useEffect(() => {
    //const intervalId = setInterval(fetchData, 500);  // Set up the interval to fetch data every 500ms

    return () => {
      //clearInterval(intervalId);  // Clear the interval when the component unmounts
    };
  }, []);

  //window.api.send('toMain', 'some data');

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