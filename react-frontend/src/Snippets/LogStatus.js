import React, {userState, useEffect } from "react";

const DoubleLogo = (props)=>{
    useEffect(()=>{
       
    });
    return (
        <div id="log_status" className="{{ navbar_text_color == 'white' and 'text-white'}} d-flex align-items-center">
            {props.authenticated &&
                <React.Fragment>
                    <img className="me-2 rounded-circle" src="{{ 'static/'+current_user.image }}" alt="user_avatar" width="32px" height="32px">
                    <Link to='/profile'><a className='px-2' href="/profile">پروفایل</a></Link>
                    <i className="border-left bg-white d-inline-block mx-2" style="width: 1px;height:10px;"></i>
                    <Link to='/logout'><a href="/logout">خروج</a></Link>
                </React.Fragment>
            ||
                <React.Fragment>
                    <i className="bi-person-fill  fs-3 me-2"></i>
                    <Link to='/login'><a href="/login">ورود</a></Link>
                    <i className="border-left bg-white d-inline-block mx-2" style="width: 1px;height:10px;"></i>
                    <Link to='/register'><a href="/register">ثبت نام</a></Link>
                </React.Fragment>
            }
        </div>
    );
}


export default DoubleLogo;