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
    <div>
      <h2>Upcoming Events</h2>
      {events.length === 0 ? (
        <p>No upcoming events found.</p>
      ) : (
        <ul>
          {events.map((event) => (
            <li key={event.id}>
              <strong>{event.summary}</strong>
              <br />
              Start: {formatDate(event.start)}
              <br />
              End: {formatDate(event.end)}
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

export default Calendar;