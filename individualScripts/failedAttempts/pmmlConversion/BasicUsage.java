// Building a model evaluator from a PMML file
Evaluator evaluator = new LoadingModelEvaluatorBuilder()
	.load(new File("ClassificationOutputTest.pmml"))
	.build();

// Perforing the self-check
evaluator.verify();

// Printing input (x1, x2, .., xn) fields
List<? extends InputField> inputFields = evaluator.getInputFields();
System.out.println("Input fields: " + inputFields);

// Printing primary result (y) field(s)
List<? extends TargetField> targetFields = evaluator.getTargetFields();
System.out.println("Target field(s): " + targetFields);

// Printing secondary result (eg. probability(y), decision(y)) fields
List<? extends OutputField> outputFields = evaluator.getOutputFields();
System.out.println("Output fields: " + outputFields);

// Iterating through columnar data (eg. a CSV file, an SQL result set)
while(true){
	// Reading a record from the data source
	Map<String, ?> inputRecord = readRecord();
	if(inputRecord == null){
		break;
	}

	Map<FieldName, FieldValue> arguments = new LinkedHashMap<>();

	// Mapping the record field-by-field from data source schema to PMML schema
	for(InputField inputField : inputFields){
		FieldName inputName = inputField.getName();

		Object rawValue = inputRecord.get(inputName.getValue());

		// Transforming an arbitrary user-supplied value to a known-good PMML value
		FieldValue inputValue = inputField.prepare(rawValue);

		arguments.put(inputName, inputValue);
	}

	// Evaluating the model with known-good arguments
	Map<FieldName, ?> results = evaluator.evaluate(arguments);

	// Decoupling results from the JPMML-Evaluator runtime environment
	Map<String, ?> resultRecord = EvaluatorUtil.decodeAll(results);

	// Writing a record to the data sink
	writeRecord(resultRecord);
}

// Making the model evaluator eligible for garbage collection
evaluator = null;