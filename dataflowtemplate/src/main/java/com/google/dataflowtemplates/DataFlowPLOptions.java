package com.google.dataflowtemplates;

import org.apache.beam.runners.dataflow.options.DataflowPipelineOptions;
import org.apache.beam.sdk.options.Default;
import org.apache.beam.sdk.options.Description;
import org.apache.beam.sdk.options.StreamingOptions;
import org.apache.beam.sdk.options.Validation.Required;

import org.apache.beam.sdk.options.ValueProvider;


public interface DataFlowPLOptions extends DataflowPipelineOptions, StreamingOptions {
    @Description("The Cloud Pub/Sub topic.")
    @Required
    ValueProvider<String> getTopic();
    void setTopic(ValueProvider<String> value);

    @Description("The directory to output files to. Must end with a slash.")
    @Required
    ValueProvider<String> getOutputDirectory();
    void setOutputDirectory(ValueProvider<String> value);

    @Description("The filename prefix of the files to write to.")
    @Default.String("output")
    @Required
    ValueProvider<String> getOutputFilenamePrefix();
    void setOutputFilenamePrefix(ValueProvider<String> value);

    @Description("The shard template of the output file. Specified as repeating sequences "
        + "of the letters 'S' or 'N' (example: SSS-NNN). These are replaced with the "
        + "shard number, or number of shards respectively")
    @Default.String("")
    ValueProvider<String> getShardTemplate();
    void setShardTemplate(ValueProvider<String> value);

    @Description("The suffix of the files to write.")
    @Default.String("")
    ValueProvider<String> getOutputFilenameSuffix();
    void setOutputFilenameSuffix(ValueProvider<String> value);

    @Description("The window duration in which data will be written. Defaults to 5s. "
        + "Allowed formats are: "
        + "Ns (for seconds, example: 5s), "
        + "Nm (for minutes, example: 12m), "
        + "Nh (for hours, example: 2h).")
    @Default.String("10s")
    String getWindowDuration();
    void setWindowDuration(String value);

    @Description("The maximum number of output shards produced when writing.")
    @Default.Integer(1)
    Integer getNumShards();
    void setNumShards(Integer value);
  }
