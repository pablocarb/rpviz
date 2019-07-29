function displaynet(network){
  var cy = cytoscape({
    container: $('#cy'),

    elements:network
  ,

  layout: {
        name: 'breadthfirst',
        roots: "node[root = 'root']"
      },

    style: [
      {
      selector: "node",
      style: {
          "background-color": '#80D0D0',
          "label": "data(name)",
          "font-size": "7px"
          }
      },
      {selector: "node[category='reactions']",
      style: {
        'background-color': '#FA8072',
        'shape': 'roundrectangle'
         }},
     {selector: "node[category='reactant']",
     style: {
       'background-color': '#52be80',
        }},
     {
      selector: 'edge',
      style: {
        'curve-style': 'bezier',
        'width': '3px',
        'target-arrow-shape': 'triangle',
      }
    }]
  });

  cy.on('mouseover','node',function(e){
    var node_select=e.target;
    molecule=node_select.data("image");
    if(molecule){
    $("#molecule").append(molecule)};
  });

  cy.on('mouseout','node',function(e){
    $("#molecule").empty();
  });

  cy.on('tap','node',function(e){
    var node_select=e.target;
    console.log(node_select.data("name"));
    link=node_select.data("link");
    if(link){
      window.open(link)
    };
  });
  };

$(function() {
  $("#selectbox").change(function(){
    value=$("#selectbox :selected").val();
    displaynet(obj[value]);
  });
});
