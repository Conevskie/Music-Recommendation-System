import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { SearchBarComponent } from './search-bar/search-bar.component';
import { MusicCardsComponent } from './music-cards/music-cards.component';
import {HttpClientModule} from "@angular/common/http";
import { BackgroundComponent } from './background/background.component';

@NgModule({
  declarations: [
    AppComponent,
    SearchBarComponent,
    MusicCardsComponent,
    BackgroundComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
