import React, { useState, useEffect } from 'react';

const Calendar = () => {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    fetchEvents();
  }, []);

  const fetchEvents = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/events');
      const data = await response.json();
      setEvents(data);
    } catch (error) {
      console.error('Error fetching events:', error);
    }
  };

  return (
    <div >
      <style>{'body { background-color: #F8DEC1; }'}</style>
      <div className='text-lg text-tab_border_brown font-mitr 'style={{marginTop:"-20px", marginLeft:"20px"}}>
        David's Calendar
      </div>
      <br />
      <h2 className='text-lg text-text_brown font-mitr ' style={{position: "fixed", left: "42%", fontSize:"15px"}}><strong>{getDate()}</strong></h2>
      {events.length === 0 ? (
        <p>No upcoming events found.</p>
      ) : (
        <ul>
          <br />
          {events.map((event) => (
            <li key={event.id}>
              
              <br />
              
              {/* if from calendar, use text-tab_border_brown; otherwise use green */}
              <div className='text-lg text-tab_border_brown font-ntr ' style={{marginTop:"-10px"}} >
              <span style={{position: "fixed", right: "55%"}}> {formatDate(event.start).substr(18, 20)} </span> 
              <span style={{position: "fixed", left: "55%"}}>{event.summary}</span>   
              </div>
              
              <br />
            </li>
          ))}
        </ul>
        
      )}
    </div>
  );
};

// Helper function to format the date
const formatDate = (dateString) => {
  const options = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: 'numeric',
    minute: 'numeric',
    timeZone: 'UTC',
  };
  return new Date(dateString).toLocaleString(undefined, options);
};

function getDate() {
  const today = new Date();
  const month = today.getMonth() + 1;
  const year = today.getFullYear();
  const date = today.getDate();
  return `${month}/${date}/${year}`;
}

export default Calendar;