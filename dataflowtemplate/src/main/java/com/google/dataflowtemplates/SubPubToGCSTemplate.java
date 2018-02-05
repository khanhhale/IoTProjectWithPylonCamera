package com.google.dataflowtemplates;

//import org.apache.beam.runners.dataflow.options.DataflowPipelineOptions;
import org.apache.beam.sdk.Pipeline;
import org.apache.beam.sdk.io.TextIO;
import org.apache.beam.sdk.io.gcp.pubsub.PubsubIO;
import org.apache.beam.sdk.options.PipelineOptionsFactory;
//import org.apache.beam.sdk.transforms.Create;
//import org.apache.beam.sdk.transforms.ParDo;
import org.apache.beam.sdk.transforms.windowing.FixedWindows;
import org.apache.beam.sdk.transforms.windowing.Window;
import org.joda.time.Duration;

import java.util.regex.Matcher;
import java.util.regex.Pattern;
/**
 */

public class SubPubToGCSTemplate 
{
  public static void main(String[] args) {
  DataFlowPLOptions opts = PipelineOptionsFactory.fromArgs(args).withValidation().as(DataFlowPLOptions.class);
  opts.setStreaming(true);
   
  System.out.println("getProject: " + opts.getProject());
  System.out.println("getGcpTempLocation: " + opts.getGcpTempLocation());
  System.out.println("getRunner: " + opts.getRunner());
  System.out.println("getDataflowJobFile: " + opts.getDataflowJobFile());
  System.out.println("getTopic: " + opts.getTopic());
  System.out.println("getOutputFilenamePrefix: " + opts.getOutputFilenamePrefix().get());
  System.out.println("getOutputFilenameSuffix: " + opts.getOutputFilenameSuffix().get());
  System.out.println("getNumShards: " + opts.getNumShards());
  System.out.println("getWindowDuration: " + opts.getWindowDuration());
  System.out.println("getShardTemplate: " + opts.getShardTemplate().get());
  Pipeline pl = Pipeline.create(opts);  

  FixedWindows window = FixedWindows.of(durationParse(opts.getWindowDuration()));
  WindowedFilenamePolicy filenamepolicy = new WindowedFilenamePolicy(opts.getOutputFilenamePrefix().get(), opts.getOutputFilenameSuffix().get());
  
  pl
    .apply("Read PubSub Events",PubsubIO.readStrings().fromTopic(opts.getTopic()))
	.apply("Window", Window.<String>into(window))
    .apply(TextIO.write().to(opts.getOutputDirectory())
    		.withFilenamePolicy(filenamepolicy)
    		.withWindowedWrites()
    		.withNumShards(opts.getNumShards()));
  pl.run();
  }
  
  private static Duration durationParse(String durationString) {
	
	  Pattern pat = Pattern.compile("[a-zA-Z]");
	  Matcher match = pat.matcher(durationString); 
	  //System.out.println("durationSring: " + durationString); 
	  
	  String durationSring = durationString.replaceAll("\\D","");  
	if(match.find()) { 
	  
      if(durationString.indexOf('s') != -1) {	   
		 return Duration.standardSeconds(Integer.valueOf(durationSring)); 
      }
      else if(durationString.indexOf('m') != -1) {
    	 return Duration.standardMinutes(Integer.valueOf(durationSring));
      }
      else if(durationString.indexOf('h') != -1) {
     	 return Duration.standardHours(Integer.valueOf(durationSring));
      }
      else if(durationString.indexOf('d') != -1) {
      	 return Duration.standardDays(Integer.valueOf(durationSring));
      }
      else {
    	 return Duration.standardMinutes(5);  
	  }
     
	}
	  else
		return Duration.standardMinutes(5);   
  }
  
}