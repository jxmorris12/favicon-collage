// jack morris 06/12/17

/*
 * FavicoApp class
 */
class FavicoApp extends React.Component {
  constructor(props) {
    super();
    this.sites = props.sites;
  }
  render() {
    console.log(this.sites);
    let children = this.sites.map(site => { return React.createElement(FavicoBox, site); });
    return React.createElement('div', {
      'className': 'favico-container'
    }, 
    children);
  }
}

/*
 * FavicoBox class
 */
class FavicoBox extends React.Component {
  constructor(props) {
    super();
    this.name = props.name;
    this.tld = props.tld;
    this.hue = props.hue;

  }
  getImageUrl() {
    if(this.hue >= 0) {
      // we have an image
      return 'http://' + this.name + '.' + this.tld + '/favicon.ico';
    } else {
      // get placeholder
      return placeholderUrl;
    }
  }
  render() {
    let innerImage = React.createElement(FavicoImage, { 'url': this.getImageUrl() });
    return React.createElement(
      "div",
      {
        'className': 'favico-box',
        'id': this.props.name
      },
      null,
      innerImage
    );
  }
}

/*
 * FavicoImage class
 */
class FavicoImage extends React.Component {
  constructor(props) {
    super();
    this.url = props.url;
  }
  render() {
    return React.createElement(
      'img',
      {
        'src': this.url,
        'className': 'favico-image'
      }
    );
  }
}

/*
 * Helper methods
 */

/*
 * Main initialization code
 */

// Sort data
topSites.sort((a,b) => { return a.hue - b.hue });
// Initialize DOM
let container = document.getElementById('container');
let reactApp = React.createElement(FavicoApp, { 'sites': topSites });
ReactDOM.render(reactApp, container);