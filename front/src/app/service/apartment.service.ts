import { Injectable } from '@angular/core';
import { Headers, Http, RequestOptions, Response } from '@angular/http';

import 'rxjs/add/operator/toPromise';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';

import { Apartment } from '../apartment';

@Injectable()
export class ApartmentService {

  private apartmentsUrl = 'api/v1/apartments/'; // Url
  private authUrl = 'api-auth/';
  private url = 'http://localhost:8000/api/v1/apartments/'

  constructor(private http: Http) { }

  getApartments(token): Observable<Apartment[]> {
    let token_string = 'Token 	' + token;
    let headers = new Headers({
      'Content-Type': 'application/json',
      'Authorization': token_string
                             });
    let options = new RequestOptions({headers: headers})
    return this.http.get(this.url, options)
               .map(this.extractApartment)
               .catch(this.handleError);
  }

  private extractApartment(res: Response) {
    let body = res.json();
    console.log(body.results);
    return body.results || {};
  }

  private handleError(error: any): Promise<any>{
    console.error("Ошибка при получении списка квартир");
    console.log(error.message || error);
    return Promise.reject(error.message || error);
  }

}
