import { useEffect, useState } from 'react';
import { supabase } from '../supabaseClient'

import checkimg from '../assets/check.png'
import checkedimg from '../assets/checked.png'

const ConfirmationItem = ({ checkimg, checkedimg, text, onClick }) => {
  const [isClicked, setIsClicked] = useState(false);

  const handleClick = () => {
    setIsClicked(!isClicked);
    onClick();
  };

  return (
    <div className="px-4 py-2 relative" style={{ marginLeft: "-18px"}}>
      <div className="flex items-center  p-4 rounded-lg h-1 " style={{width:"300px"}}>
        <div className="flex-shrink-0 mr-4">
          <button className="focus:outline-none" onClick={handleClick}>
            <img src={isClicked ? checkedimg : checkimg} alt="checkbox" className="w-5 h-6 object-contain" />
          </button>
        </div>
        <div className="flex-grow">
          <span className="text-lg text-text_brown font-ntr"style={{fontSize: "15px", marginLeft: "-8px"}}>{text}</span>
        </div>
      </div>
    </div>
  );
};

const ToDoList = () => {
  const [todos, setTodos] = useState([]);

  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    const { data, error } = await supabase
      .from('items')
      .select('*');

    if (error) {
      console.error('Error fetching todos:', error);
    } else {
      setTodos(data);
    }
  };

  const handleItemClick = (id) => {
    // Handle the click event for each todo item
    console.log(`Clicked on todo with ID: ${id}`);
  };

  return (
    <div>
      <style>{'body { background-color: #F8DEC1; }'}</style>
      <div className='text-lg text-tab_border_brown font-mitr 'style={{marginTop:"-20px", marginLeft:"20px"}}>
        David's To-Do's
      </div>
      <div className=" px-4 py-2" >
        {todos.map((todo) => (
          <ConfirmationItem
            checkimg={checkimg}
            checkedimg={checkedimg}
            text={todo.description}
            onClick={() => handleItemClick(todo.id)}
          />
        ))}
      </div>
    </div>
  );
};

export default ToDoList;