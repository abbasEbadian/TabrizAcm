import React, { useState, useEffect } from 'react';
import {BrowserRouter as Router, Switch, Route, Link} from 'react-router-dom';
import Home from './Pages/Home.js' ;
import About from './Pages/About.js' ;
import Profile from './Pages/Profile.js' ;
import Contact from './Pages/Contact.js' ;
import Login from './Pages/Login.js' ;
import Register from './Pages/Register.js' ;
import Logout from './Pages/Logout.js' ;
import logo from './logo.svg';
import './App.css';

function App() {
  const [count, setCount] = useState(0) ;
  const [authenticated, setAuthenticated] = useState(false);
  useEffect(()=>{
    fetch("is_authenticated").then(r=>{
        r.json().then(d=>{
          setAuthenticated(d.is_authenticated);
      });
    });
  })
  const logout = ()=>{
    setAuthenticated(false);
  }
  return (
      <Router>
        <Switch>
          <Route path="/" exact render={()=><Home authenticated={authenticated} title="PCPC - Home" />}/>
          <Route path="/about-us" exact render={()=><About authenticated={authenticated} title="PCPC - about"/>}/>
          <Route path="/profile" exact render={()=><Profile authenticated={authenticated} title="PCPC - profile"/>}/>
          <Route path="/contact" exact render={()=><Contact authenticated={authenticated} title="PCPC - contact"/>} />
          <Route path="/login" exact render={()=><Login authenticated={authenticated} title="PCPC - login"/> }/>
          <Route path="/register" exact render={()=><Register authenticated={authenticated}  title="PCPC - contact"/>}/>
          <Route path="/logout" exact render={()=><Logout _authenticated={authenticated} logout={logout} />} />
        </Switch>
      </Router>
  );
}

export default App;
