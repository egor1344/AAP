export class Apartment {
  id: number;
  title: string;
  link: string;
  price: number;
  city: string;
  date_time: string;
  site: string;

}

export class ApartmentFull {
  id: number;
  title: string;
  link: string;
  price: number;
  city: string;
  date_time: string;
  site: string;
  price_m2 : number;
  agent : string;
  address : string;
  floor : string;
  living_space : string;
  rooms : string;
  district : string;
  type_house : string;
  active : boolean;
}
