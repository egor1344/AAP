import { AapPage } from './app.po';

describe('aap App', () => {
  let page: AapPage;

  beforeEach(() => {
    page = new AapPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
