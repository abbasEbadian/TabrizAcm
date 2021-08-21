import React from "react";
import LogStatus from './LogStatus';
import DoubleLogo from './DoubleLogo';
import DoubleLogoWhite from './DoubleLogoWhite';
import {Link} from 'react-router-dom';

const Nav = (props)=>{
    
    return (
        <nav className="nav justify-content-between align-items-center  px-md-5 px-sm-3 ">
            <LogStatus/>
            <Link to='/'><a className="ms-5 text-white" href="/">صفحه اصلی</a></Link>
            <Link to='/contact-us'><a className="ms-5 text-white" href="/contact-us">ارتباط با ما</a></Link>
            <Link to='/about-us'><a className="me-auto ms-5 text-white" href="/about-us">درباره ما</a></Link>
            {props.navbar_logo_color === 'white' ?
                <DoubleLogoWhite />
            :
                <DoubleLogo />
            }

        </nav>
    );
}


export default Nav;