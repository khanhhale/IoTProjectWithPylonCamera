package com.google.dataflowtemplates;

import org.apache.beam.sdk.io.DefaultFilenamePolicy;
import org.apache.beam.sdk.io.FileBasedSink.FilenamePolicy;
import org.apache.beam.sdk.io.fs.ResolveOptions.StandardResolveOptions;
import org.apache.beam.sdk.io.fs.ResourceId;
import org.apache.beam.sdk.options.ValueProvider;
import org.apache.beam.sdk.options.ValueProvider.StaticValueProvider;
import org.apache.beam.sdk.repackaged.org.apache.commons.lang3.StringUtils;
import org.joda.time.DateTimeZone;
import org.joda.time.Instant;
import org.joda.time.format.DateTimeFormat;
import org.joda.time.format.ISODateTimeFormat;
import org.joda.time.format.*;



@SuppressWarnings("serial")
public class WindowedFilenamePolicy extends FilenamePolicy {

    /**
     * Possible sub-directory creation modes.
     */
    public static enum SubDirectoryPolicy {
        NONE("."),
        PER_HOUR("yyyy-MM-dd/HH"),
        PER_DAY("yyyy-MM-dd");

        private final String subDirectoryPattern;

        private SubDirectoryPolicy(String subDirectoryPattern) {
            this.subDirectoryPattern = subDirectoryPattern;
        }

        public String getSubDirectoryPattern() {
            return subDirectoryPattern;
        }

        public String format(Instant instant) {
            DateTimeFormatter formatter = DateTimeFormat.forPattern(subDirectoryPattern);
            return formatter.print(instant);
        }
    }

    /**
     * The formatter used to format the window timestamp for outputting to the filename.
     */
    private static final DateTimeFormatter formatter = ISODateTimeFormat
            .basicDateTimeNoMillis()
            .withZone(DateTimeZone.getDefault());

    /**
     * The filename prefix.
     */
    private final ValueProvider<String> prefix;

    /**
     * The filenmae suffix.
     */
    private final ValueProvider<String> suffix;

    /**
     * The shard template used during file formatting.
     */
    private final ValueProvider<String> shardTemplate;

    /**
     * The policy which dictates when or if sub-directories are created
     * for the windowed file output.
     */
    private ValueProvider<SubDirectoryPolicy> subDirectoryPolicy = StaticValueProvider.of(SubDirectoryPolicy.NONE);

    /**
     * Constructs a new {@link WindowedFilenamePolicy} with the
     * supplied prefix used for output files.
     * 
     * @param prefix    The prefix to append to all files output by the policy.
     * @param shardTemplate The template used to create uniquely named sharded files.
     * @param suffix    The suffix to append to all files output by the policy.
     */
    public WindowedFilenamePolicy(String prefix, String shardTemplate, String suffix) {
        this(StaticValueProvider.of(prefix), 
                StaticValueProvider.of(shardTemplate),
                StaticValueProvider.of(suffix));
    }

    /**
     * Constructs a new {@link WindowedFilenamePolicy} with the
     * supplied prefix used for output files.
     * 
     * @param prefix    The prefix to append to all files output by the policy.
     * @param shardTemplate The template used to create uniquely named sharded files.
     * @param suffix    The suffix to append to all files output by the policy.
     */
    public WindowedFilenamePolicy(
            ValueProvider<String> prefix, 
            ValueProvider<String> shardTemplate, 
            ValueProvider<String> suffix) {
        this.prefix = prefix;
        this.shardTemplate = shardTemplate;
        this.suffix = suffix; 
    }

    /**
     * The subdirectory policy will create sub-directories on the
     * filesystem based on the window which has fired.
     * 
     * @param policy    The subdirectory policy to apply.
     * @return The filename policy instance.
     */
    public WindowedFilenamePolicy withSubDirectoryPolicy(SubDirectoryPolicy policy) {
        return withSubDirectoryPolicy(StaticValueProvider.of(policy));
    }

    /**
     * The subdirectory policy will create sub-directories on the
     * filesystem based on the window which has fired.
     * 
     * @param policy    The subdirectory policy to apply.
     * @return The filename policy instance.
     */
    public WindowedFilenamePolicy withSubDirectoryPolicy(ValueProvider<SubDirectoryPolicy> policy) {
        this.subDirectoryPolicy = policy;
        return this;
    }

    /**
     * The windowed filename method will construct filenames per window in the
     * format of output-yyyyMMdd'T'HHmmss-001-of-100.txt.
     */
    @Override
    public ResourceId windowedFilename(ResourceId outputDirectory, WindowedContext c, String extension) {
        Instant windowInstant = c.getWindow().maxTimestamp();
        String datetimeStr = formatter.print(windowInstant.toDateTime());

        // Remove the prefix when it is null so we don't append the literal 'null'
        // to the start of the filename
        String filenamePrefix = prefix.get() == null ? datetimeStr : prefix.get() + "-" + datetimeStr;
        String filename = DefaultFilenamePolicy.constructName(
                filenamePrefix, 
                shardTemplate.get(), 
                StringUtils.defaultIfBlank(suffix.get(), extension),  // Ignore the extension in favor of the suffix.
                c.getShardNumber(), 
                c.getNumShards());

        String subDirectory = subDirectoryPolicy.get().format(windowInstant);
        return outputDirectory
                .resolve(subDirectory, StandardResolveOptions.RESOLVE_DIRECTORY)
                .resolve(filename, StandardResolveOptions.RESOLVE_FILE);
    }

    /**
     * Unwindowed writes are unsupported by this filename policy so an {@link UnsupportedOperationException}
     * will be thrown if invoked.
     */
    @Override
    public ResourceId unwindowedFilename(ResourceId outputDirectory, Context c, String extension) {
    throw new UnsupportedOperationException("There is no windowed filename policy for unwindowed file"
        + " output. Please use the WindowedFilenamePolicy with windowed writes or switch filename policies.");
    }
}
