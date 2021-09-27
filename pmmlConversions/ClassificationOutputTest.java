package org.jpmml.evaluator.tree;

import java.util.Arrays;
import java.util.Map;

import org.dmg.pmml.FieldName;
import org.jpmml.evaluator.Configuration;
import org.jpmml.evaluator.ConfigurationBuilder;
import org.jpmml.evaluator.ModelEvaluator;
import org.jpmml.evaluator.ModelEvaluatorTest;
import org.jpmml.evaluator.OutputFilters;
import org.junit.Test;

import static org.junit.Assert.assertEquals;

public class ClassificationOutputTest extends ModelEvaluatorTest {

	@Test
	public void evaluate() throws Exception {
		ConfigurationBuilder configurationBuilder = new ConfigurationBuilder();

		Configuration configuration = configurationBuilder.build();

		ModelEvaluator<?> evaluator = createModelEvaluator(configuration);

		checkResultFields(Arrays.asList("result"), Arrays.asList("output_predictedValue", "output_predictedDisplayValue", "output_probability"), evaluator);

		Map<FieldName, ?> arguments = createArguments("flag", false);

		Map<FieldName, ?> results = evaluator.evaluate(arguments);

		assertEquals(1 + 3, results.size());

		assertEquals("0", getTarget(results, "result"));

		assertEquals("0", getOutput(results, "output_predictedValue"));
		assertEquals("zero", getOutput(results, "output_predictedDisplayValue"));
		assertEquals(1d, getOutput(results, "output_probability"));

		configurationBuilder.setOutputFilter(OutputFilters.KEEP_FINAL_RESULTS);

		configuration = configurationBuilder.build();

		evaluator.configure(configuration);

		checkResultFields(Arrays.asList("result"), Arrays.asList("output_predictedDisplayValue", "output_probability"), evaluator);

		results = evaluator.evaluate(arguments);

		assertEquals(1 + 2, results.size());
	}
}