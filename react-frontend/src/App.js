import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
  const [count, setCount] = useState(0) ;
  useEffect(()=>{
    fetch("/api").then(response =>{
      response.json().then(data=>{
        setCount(data.count);
      });
    });
  }, []);
  function addcount(e) {
    setCount(+count + 1);
  }
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
          Number is {count}
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React or 
          
        </a>
        <button onClick={ addcount }> Add up to count</button>
      </header>
    </div>
  );
}

export default App;
