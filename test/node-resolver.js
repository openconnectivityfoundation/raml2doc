
//https://github.com/BigstickCarpet/json-schema-ref-parser/blob/master/docs/README.md
var $RefParser = require('json-schema-ref-parser');

//$RefParser.bundle(process.argv[2])
$RefParser.dereference(process.argv[2])
  .then(function(schema) {
    console.log(JSON.stringify(schema));
  });
