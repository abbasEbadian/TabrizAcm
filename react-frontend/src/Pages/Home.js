import React, {useState, useEffect} from "react";


const Home = (props)=>{
    useEffect(()=>{
        document.title = props.title;
    }, []);
    return <h1> Home </h1>
}


export default Home;