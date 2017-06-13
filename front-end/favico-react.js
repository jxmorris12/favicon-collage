// jack morris 06/12/17


/*
 * FavicoBox class
 */
class FavicoBox extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    return React.createElement(
      "div",
      {
        'class': 'favico-box'
      },
      "Hello ",
      this.props.name
    );
  }
}


/*
 * Main initialization code
 */
let container = document.getElementById('container');
ReactDOM.render(React.createElement(FavicoBox, { name: "John" }), container);