import React from 'react';
import { Link, useLocation } from 'react-router-dom'
import calendar from '../assets/calendar.png'
import chat from '../assets/chat.png'
import todo from '../assets/todo.png'

function Navigation() {
  const location = useLocation();

  return (
    <nav className="flex justify-end">
      <ul className="flex space-x-4">
        <li>
          <Link to="/">
            <img
              src={chat}
              className={`h-6 w-6 ${location.pathname === '/' ? 'border-2 border-borderbrown-600 rounded-lg' : ''}`}
              alt="Chat"
            />
          </Link>
        </li>
        <li>
          <Link to="/cal">
            <img
              src={calendar}
              className={`h-6 w-6 ${location.pathname === '/cal' ? 'border-2 border-borderbrown-600 rounded-lg ' : ''}`}
              alt="Calendar"
            />
          </Link>
        </li>
        <li>
          <Link to="/todo">
            <img
              src={todo}
              className={`h-6 w-6 ${location.pathname === '/todo' ? 'border-2 border-borderbrown-600 rounded-lg' : ''}`}
              alt="Todo"
            />
          </Link>
        </li>
      </ul>
    </nav>
  );
}

export default Navigation;