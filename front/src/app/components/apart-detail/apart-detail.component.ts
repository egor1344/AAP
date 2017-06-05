import 'rxjs/add/operator/switchMap';
import 'rxjs/add/operator/map';

import { Observable } from 'rxjs/Observable';
import { Component, OnInit }      from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import { Location }               from '@angular/common';

import { ApartmentService } from '../../service/apartment.service';
import { ApartmentFull } from "../../apartment";


@Component({
  selector: 'app-apart-detail',
  templateUrl: './apart-detail.component.html',
  styleUrls: ['./apart-detail.component.css']
})
export class ApartDetailComponent implements OnInit {

  apartment: ApartmentFull;
  id: number;

  constructor(
    private route: ActivatedRoute,
    private location: Location,
    private apartmentService: ApartmentService
  ) { }

  ngOnInit() {
    this.getApartmentDetail();
  }

  getApartmentDetail(){
    this.route.params
       .switchMap((params: Params) => {
         this.id = +params['id'];
         return this.apartmentService.getApartmentDetail(this.id);
       }).subscribe(take_apartment => {
         this.apartment = take_apartment;
         this.readProp(this.apartment);
       });
  }

  readProp(aparment){
    console.log(aparment.title);
  }

}
