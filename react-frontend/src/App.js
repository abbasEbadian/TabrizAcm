import React, { useState, useEffect } from 'react';
import {BrowserRouter as Router, Switch, Route, Link} from 'react-router-dom';
import Home from './Pages/Home.js' ;
import About from './Pages/About.js' ;
import Profile from './Pages/Profile.js' ;
import Contact from './Pages/Contact.js' ;
import Login from './Pages/Login.js' ;
import Register from './Pages/Register.js' ;
import logo from './logo.svg';
import {logout, useAuth} from "./auth";
import './App.css';

function App() {
  const [count, setCount] = useState(0) ;
  const [authenticated,] = useAuth(false);
  const _logout = ()=>{
    logout();
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
          <Route path="/logout" exact render={()=>{_logout()}} />
        </Switch>
      </Router>
  );
}

export default App;
