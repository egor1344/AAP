import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ApartDetailComponent } from './apart-detail.component';

describe('ApartDetailComponent', () => {
  let component: ApartDetailComponent;
  let fixture: ComponentFixture<ApartDetailComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ApartDetailComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ApartDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
