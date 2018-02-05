package com.google.dataflowtemplates;
import org.apache.beam.sdk.io.FileBasedSink.FilenamePolicy;
import org.apache.beam.sdk.io.fs.ResolveOptions.StandardResolveOptions;
import org.apache.beam.sdk.io.fs.ResourceId;
import org.apache.beam.sdk.transforms.display.DisplayData;

public class WindowedFilenamePolicy extends FilenamePolicy{
	private static final long serialVersionUID = 1L;
	final String outputFilePrefix;
	final String outputFileSuffix;

    WindowedFilenamePolicy(String outputFilePrefix, String outputFileSuffix) {
        this.outputFilePrefix = outputFilePrefix;
        this.outputFileSuffix = outputFileSuffix;
    }
    @Override
    public ResourceId windowedFilename(ResourceId outputDirectory, WindowedContext input, String extension) {
        String filename = String.format(
                "%s-%s-%s-of-%s-pane-%s%s%s%s",
                outputFilePrefix,
                input.getWindow(),
                input.getShardNumber(),
                input.getNumShards() - 1,
                input.getPaneInfo().getIndex(),
                input.getPaneInfo().isLast() ? "-final" : "",
                outputFileSuffix,		                   
                extension);
        return outputDirectory.resolve(filename, StandardResolveOptions.RESOLVE_FILE);
    }
    @Override
    public ResourceId unwindowedFilename(ResourceId outputDirectory, Context input, String extension) {
        throw new UnsupportedOperationException("Expecting windowed outputs only");
    }
    @Override
    public void populateDisplayData(DisplayData.Builder builder) {
    	builder.add(DisplayData.item("fileNamePrefix", outputFilePrefix).withLabel("File Name Prefix"));
    }

}
