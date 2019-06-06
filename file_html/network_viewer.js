$(function() {
  var cy = cytoscape({
    container: $('#cy'),
    elements:ntElements
  ,

  layout: {
        name: 'grid',
        columns:3,
        position : function(ele){
          if(ele.data('category')==='reactant'){
            return{col:0};
          }
          else if(ele.data('category')==='product'){
            return{col:2};
          }
          return {col:1};
        }
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
    $("#molecule").attr('src',molecule);
    $("#molecule").css(
      {"width":"200px",
       "height":"200px"});}

      })

    //alert(node_select.data("image"));
  cy.on('mouseout','node',function(e){
    $("#molecule").attr('src',"");
    $("#molecule").css({
      "width":"",
      "height":""});
  });
})