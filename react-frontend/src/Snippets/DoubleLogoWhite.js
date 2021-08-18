import React from "react";

const DoubleLogoWhite = (props)=>{
    return (
        <div className="d-flex justify-content-center align-items-end" id="logo_container">
            <img src={process.env.PUBLIC_URL + "/img/pcpc-white.png"} alt="logo" className="logo_img"/>
            <img src={process.env.PUBLIC_URL + '/img/white-logo.png'} alt="logo" className="logo_img"/>
     </div>  
    );
}


export default DoubleLogoWhite;