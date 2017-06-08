import { Injectable } from '@angular/core';
import { Headers, Http, RequestOptions, Response } from '@angular/http';

import 'rxjs/add/operator/toPromise';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';

import { Apartment, ApartmentFull } from '../apartment';
import { AuthService } from './auth.service';

@Injectable()
export class ApartmentService {

  private apartmentsUrl = 'api/v1/apartments/?page='; // Url
  private authUrl = 'api-auth/';
  private url = 'api/v1/apartments/'

  constructor(
    private http: Http,
    private authService: AuthService
  ) { }

  getApartments(num): Observable<any> {
    let token = this.authService.getToken()
    token = 'Token 	' + token;
    let headers = new Headers({
      'Content-Type': 'application/json',
      'Authorization': token,
      'Access-Control-Allow-Origin': '*'
                             });
    let options = new RequestOptions({headers: headers})
    return this.http.get(this.apartmentsUrl + num, options)
               .map(this.extractApartment)
               .catch(this.handleError);
  }

  getApartmentDetail(id): Observable<ApartmentFull>{
    // console.log('id = ' + id);
    let token = this.authService.getToken()
    token = 'Token 	' + token;
    let headers = new Headers({
      'Content-Type': 'application/json',
      'Authorization': token
                             });
    let url = this.url + id + '/';
    console.log(typeof(id));
    console.log('url = ', url);
    let options = new RequestOptions({headers: headers})
    return this.http.get(url, options)
                .map(this.extractApartment)
                .catch(this.handleError);
  }

  private extractApartment(res: Response) {
    let body = res.json();
    return body;
  }

  private handleError(error: any): Promise<any>{
    console.error("Ошибка при получении списка квартир");
    console.log(error.message || error);
    return Promise.reject(error.message || error);
  }

}
