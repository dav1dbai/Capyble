import React, { useState, useEffect } from 'react';

const Calendar = () => {
  const [events, setEvents] = useState([]);
  const [currentDate, setCurrentDate] = useState(new Date());

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

  const nextDate = () => {
    const newDate = new Date(currentDate.setDate(currentDate.getDate() + 1));
    setCurrentDate(new Date(newDate)); // Update state to the next day
  };

  const lastDate = () => {
    const newDate = new Date(currentDate.setDate(currentDate.getDate() - 1));
    setCurrentDate(new Date(newDate)); // Update state to the next day
  };

  return (
    <div >
      <style>{'body { background-color: #F8DEC1; }'}</style>
      <div className='text-lg text-tab_border_brown font-mitr 'style={{marginTop:"-20px", marginLeft:"20px"}}>
        David's Calendar
      </div>
      <h2 className='text-lg text-text_brown font-mitr ' style={{position: "relative", left: "37%",top: "12%", fontSize:"15px" }}><strong>{currentDate.toLocaleDateString()}</strong></h2>
      {events.length === 0 ? (
        <p className='text-lg text-tab_border_brown font-ntr ' style={{position: "relative", left: "17%",top: "20%"}}> No upcoming events found.</p>
      ) : (

        <ul >
          <br />
          {events.map((event) => (
            <li key={event.id}>
              
              <br />
              
              {/* if from calendar, use text-tab_border_brown; otherwise use green */}
              <div className='text-lg text-tab_border_brown font-ntr ' style={{marginTop:"-45px"}} >
              <span style={{position: "relative", right: "-60px"}}> {formatDate(event.start).substr(18, 20)} </span> 
              <span style={{position: "relative", left: "70px"}}>{event.summary}</span>   
              </div>
              
              <br />
            </li>
          ))}
        </ul>
        
      )}
      <div  style={{position: "fixed", left: "35%",top: "90%", fontSize:"15px"}}>
      <button onClick={lastDate}>Back |</button> {" "}
      <button onClick={nextDate}>| Next</button>

      </div>
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



function todayList(events) {

  // Prepare list items using a for loop
  let todayevents = [];
  let todayevents_start = [];
  let now = new Date()
  for (let i = 0; i < events.length; i++) {
    if(events.start.substr(0, 12) == now){
      todayevents.push(events[i].summary);
      todayevents_start.push(events[i].start);
    }
  }

  return (
    <ul></ul>
  );
}

export default Calendar;