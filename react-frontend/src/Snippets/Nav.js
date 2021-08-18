import React from "react";
import LogStatus from './LogStatus';
import DoubleLogo from './DoubleLogo';
import DoubleLogoWhite from './DoubleLogoWhite';

const Nav = (props)=>{
    
    return (
        <nav class="nav justify-content-between align-items-center  px-md-5 px-sm-3 {{ navbar_text_color == 'white' and 'white_theme' }}">
        <LogStatus authenticated={props.authenticated}/>
        <Link to='/'><a class="ms-5 text-white" href="/">صفحه اصلی</a></Link>
        <Link to='/contact-us'><a class="ms-5 text-white" href="/contact-us">ارتباط با ما</a></Link>
        <Link to='/about-us'><a class="me-auto ms-5 text-white" href="/about-us">درباره ما</a></Link>
        {props.navbar_logo_color == 'white' ?
            <DoubleLogoWhite />
        :
            <DoubleLogo />
        }

    </nav>
    );
}


export default Nav;