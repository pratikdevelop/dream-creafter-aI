import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DreamHistoryComponent } from './dream-history.component';

describe('DreamDisplayComponent', () => {
  let component: DreamHistoryComponent;
  let fixture: ComponentFixture<DreamHistoryComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DreamHistoryComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DreamHistoryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
