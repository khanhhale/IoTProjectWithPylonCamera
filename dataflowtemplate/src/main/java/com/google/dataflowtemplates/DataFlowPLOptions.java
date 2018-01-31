package com.google.dataflowtemplates;

import org.apache.beam.runners.dataflow.options.DataflowPipelineOptions;
import org.apache.beam.sdk.options.Default;
import org.apache.beam.sdk.options.Description;
import org.apache.beam.sdk.options.StreamingOptions;
import org.apache.beam.sdk.options.Validation.Required;

import com.google.dataflowtemplates.WindowedFilenamePolicy.SubDirectoryPolicy;

import org.apache.beam.sdk.options.ValueProvider;


public interface DataFlowPLOptions extends DataflowPipelineOptions, StreamingOptions {
    @Description("The Cloud Pub/Sub topic.")
    @Required
    ValueProvider<String> getTopic();
    void setTopic(ValueProvider<String> value);

    @Description("The directory to output the files to.")
    @Required
    ValueProvider<String> getOutputDirectory();
    void setOutputDirectory(ValueProvider<String> value);

    @Description("The prefix of the output files.")
    @Default.String("output")
    @Required
    ValueProvider<String> getOutputFilenamePrefix();
    void setOutputFilenamePrefix(ValueProvider<String> value);

    @Description("The shard template specified as repeating sequences "
        + "of the letters 'S' or 'N' (example: SSS-NNN). These are replaced with the "
        + "shard number, or number of shards respectively")
    @Default.String("")
    ValueProvider<String> getShardTemplate();
    void setShardTemplate(ValueProvider<String> value);

    @Description("The suffix of the output files.")
    @Default.String("")
    ValueProvider<String> getOutputFilenameSuffix();
    void setOutputFilenameSuffix(ValueProvider<String> value);

    @Description("The sub-directory policy which files will use when dataflow output the files per window.")
    @Default.Enum("NONE")
    SubDirectoryPolicy getSubDirectoryPolicy();
    void setSubDirectoryPolicy(SubDirectoryPolicy value);

    @Description("The window duration in which data will be written. Defaults to 30 seconds. "
        + "The allowed formats are in Ns, Nm, Nh or Nd where N stands for any number and the letter that follows N indicates time in second, minute, hour or day "
        + "Ns (for seconds, 5s), "
        + "Nm (for minutes, 5m), "
        + "Nh (for hours, 5h)."
        + "Nd (for days, 5d).")
    @Default.String("30s")
    String getWindowDuration();
    void setWindowDuration(String value);

    @Description("The maximum number of output shards produced.")
    @Default.Integer(1)
    Integer getNumShards();
    void setNumShards(Integer value);
  }
