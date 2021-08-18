import React from "react";

const DoubleLogo = (props)=>{
    return (
        <div className="d-flex justify-content-center align-items-end " id="logo_container">
            <img src={process.env.PUBLIC_URL + "/img/pcpc.png"} alt="logo" className="logo_img"/>
            <img src={process.env.PUBLIC_URL + '/img/colored-logo.png'} alt="logo" className="logo_img"/>
        </div>
    );
}


export default DoubleLogo;