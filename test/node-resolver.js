
//https://github.com/BigstickCarpet/json-schema-ref-parser/blob/master/docs/README.md
var $RefParser = require('json-schema-ref-parser');
var resolveAllOf = require('json-schema-resolve-allof');

//$RefParser.bundle(process.argv[2])
$RefParser.dereference(process.argv[2])
  .then(function(schema) {
    data = resolveAllOf(schema);
    console.log(JSON.stringify(data));
  });
