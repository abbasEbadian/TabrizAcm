import React, {useEffect, useState } from "react";
import { Redirect } from 'react-router-dom';
const Logout = (props)=>{
    const {_authenticated, logout} = props;
    const [authenticated, setAuthenticated ] =  useState(_authenticated);
    useEffect(()=>{
        console.log(authenticated);
        
        if(authenticated){
            fetch('/logout').then(response=>{   
                response.json().then(data=>{
                    if (data.result === "success"){
                        props.logout();
                    }
                })
            });
        }
    }, []);
    if (!authenticated) {
        return <Redirect to='/'/>;
    }
    return (
        <React.Fragment>

        </React.Fragment>
    );
}


export default Logout;