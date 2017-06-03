import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { StatisticaComponent } from './statistica.component';

describe('StatisticaComponent', () => {
  let component: StatisticaComponent;
  let fixture: ComponentFixture<StatisticaComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ StatisticaComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(StatisticaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
