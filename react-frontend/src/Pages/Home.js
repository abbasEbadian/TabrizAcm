import React, {useState, useEffect} from "react";
import Navbar from "../Snippets/Nav";

const Home = (props)=>{
    useEffect(()=>{
        document.title = props.title;
    }, []);
    return (
        <React.Fragment>
            <Navbar></Navbar>
        </React.Fragment>
    );
}


export default Home;