import { Injectable } from '@angular/core';
import { Http, Headers } from '@angular/http';
import 'rxjs/add/operator/map';

@Injectable()
export class AuthService {

  authToken: any;
  user: any;


  constructor(
    private http: Http
  ) { }

  registerUser(user){
    let headers = new Headers();
    headers.append('Content-Type', 'application/json');
    return this.http.post('rest-auth/registration/', user, {headers: headers})
    .map(res => res.json());
  }

  authenticateUser(user) {
    let headers = new Headers();
    headers.append('Content-Type', 'application/json');
    // console.log(user);
    return this.http.post('rest-auth/login/', user, {headers: headers})
    .map(res => res.json());
  }

  getProfile(){
    let headers = new Headers();
    this.loadToken();
    headers.append('Authorization', this.authToken);
    headers.append('Content-Type', 'application/json');
    return this.http.post('http://localhost:3000/users/profile', {headers: headers})
    .map(res => res.json());
  }

  storeUserData(token, user){
    // console.log('store user');
    localStorage.setItem('id_token', token);
    localStorage.setItem('user', JSON.stringify(user));
    this.authToken = token;
    this.user = user;
  }

  loadToken(){
    const token = localStorage.getItem('id_token');
    this.authToken = token;
  }

  getUser(){
    return localStorage.getItem('user');
  }

  getToken(){
    this.loadToken()
    return this.authToken;
  }

  logout() {
    // console.log('Logout = ' + this.authToken + ' ' + this.user);
    // console.log(localStorage);
    this.authToken = null;
    this.user = null;
    localStorage.clear()
    // console.log(localStorage);
  }

  isLogin(){
    let isLogin = !!localStorage.getItem('id_token');
    return isLogin;
  }

}
